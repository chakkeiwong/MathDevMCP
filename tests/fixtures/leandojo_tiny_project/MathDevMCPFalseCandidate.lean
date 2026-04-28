theorem mathdevmcp_tiny_false_candidate (a b : Nat) : a + b = a := by
  exact Nat.add_comm a b
