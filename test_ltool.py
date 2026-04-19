# test_ltool.py
import language_tool_python
tool = language_tool_python.LanguageTool('en-US')
matches = tool.check("This are bad grammar.")
print(f"Found {len(matches)} grammar issues")