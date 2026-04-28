theorem mathdevmcp_tiny_true (a b : Nat) : a + b = b + a := by
  exact Nat.add_comm a b
