# Add Styling Options

1. Extend the style object accepted by `/factory/generate` to support fonts, colors, and spacing options in addition to indent and header_comment.
2. Update `app/services/codegen.py` to read these style settings and apply them during Swift code generation.
3. Document the new style parameters in `README.md` with examples.
4. Write tests verifying that style options correctly affect generated code.
