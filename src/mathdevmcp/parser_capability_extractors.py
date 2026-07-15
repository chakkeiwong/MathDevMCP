import json
import re
import xml.etree.ElementTree as ET


def _p02r2_extract_latexml_structural_label_set(specialist_output_xml, specialist_log):
    if type(specialist_output_xml) is not bytes or type(specialist_log) is not bytes:
        raise ValueError("LaTeXML extractor inputs must be bytes")
    try:
        xml_text = specialist_output_xml.decode("utf-8", "strict")
        log_text = specialist_log.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise ValueError("LaTeXML artifacts must be strict UTF-8") from exc
    for line in log_text.split("\n"):
        if line.startswith("Error:") or "undefined environment" in line or "undefined-environment" in line:
            raise ValueError("LaTeXML log reports malformed output")
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ValueError("LaTeXML output is malformed XML") from exc
    labels = []
    for element in root.iter():
        if type(element.tag) is not str:
            raise ValueError("LaTeXML element tag must be a string")
        if element.tag.rsplit("}", 1)[-1] == "ERROR":
            raise ValueError("LaTeXML output contains an error element")
        for name, value in element.attrib.items():
            if type(name) is not str or type(value) is not str:
                raise ValueError("LaTeXML attributes must be strings")
            if name.rsplit("}", 1)[-1] == "labels":
                for token in value.split():
                    if token.startswith("LABEL:"):
                        label = token.split("LABEL:", 1)[1]
                        if not label or label in labels:
                            raise ValueError("LaTeXML labels must be nonempty and unique")
                        labels.append(label)
    return {"raw_observable_field": "document_structural_label_set", "observed_value": sorted(labels)}


def _p02r2_extract_pandoc_math_label_set(specialist_stdout_json):
    if type(specialist_stdout_json) is not bytes:
        raise ValueError("Pandoc extractor input must be bytes")
    try:
        text = specialist_stdout_json.decode("utf-8", "strict")
        document = json.loads(text)
    except (UnicodeDecodeError, ValueError) as exc:
        raise ValueError("Pandoc output must be strict UTF-8 JSON") from exc
    if type(document) is not dict:
        raise ValueError("Pandoc output root must be an object")
    if set(document) != {"blocks", "meta", "pandoc-api-version"}:
        raise ValueError("Pandoc output root has the wrong shape")
    if type(document["blocks"]) is not list or type(document["meta"]) is not dict:
        raise ValueError("Pandoc output collections have the wrong shape")
    if type(document["pandoc-api-version"]) is not list or not document["pandoc-api-version"]:
        raise ValueError("Pandoc API version has the wrong shape")
    labels = set()
    stack = [document]
    while stack:
        value = stack.pop()
        if type(value) is dict:
            node_type = None
            content = None
            for key, item in value.items():
                if type(key) is not str:
                    raise ValueError("Pandoc object keys must be strings")
                if key == "t":
                    node_type = item
                if key == "c":
                    content = item
            if node_type is not None and type(node_type) is not str:
                raise ValueError("Pandoc node type must be a string")
            if node_type == "Math":
                if type(content) is not list or len(content) != 2:
                    raise ValueError("Pandoc Math node has the wrong shape")
                math_kind = content[0]
                payload = content[1]
                if type(math_kind) is not dict or set(math_kind) != {"t"}:
                    raise ValueError("Pandoc Math kind has the wrong shape")
                if type(math_kind["t"]) is not str or math_kind["t"] not in ("InlineMath", "DisplayMath"):
                    raise ValueError("Pandoc Math kind is invalid")
                if type(payload) is not str:
                    raise ValueError("Pandoc Math payload must be a string")
                for match in re.finditer(r"\\label\s*\{([^{}]+)\}", payload):
                    label = match.group(1)
                    if not label or label in labels:
                        raise ValueError("Pandoc labels must be nonempty and unique")
                    labels.add(label)
            else:
                for key, item in value.items():
                    if key != "t":
                        stack.append(item)
        elif type(value) is list:
            stack.extend(value)
        elif type(value) is str:
            value = value
    return {"raw_observable_field": "document_structural_label_set", "observed_value": sorted(labels)}
