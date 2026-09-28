# Extending

Implement `Action` with `name`, `validate`, `plan`, and `execute`; optionally implement `compensate`. Register the instance in `openops/actions/builtin.py` for the reference build.

Keep external credentials out of action payloads. Prefer secret references and adapter-specific secret stores. New integrations should preserve the control flow: proposal → validation → policy → risk → approval → execution → audit.
