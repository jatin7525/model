from marshmallow import Schema, fields

class ChatInputSchema(Schema):
    prompt = fields.Str(required=True, metadata={"description": "Prompt to send to the LLM"})
    passcode = fields.Str(required=False, metadata={"description": "6-digit passcode"})


class ImageInputSchema(Schema):
    prompt = fields.Str(required=True, metadata={"description": "Prompt for image generation"})
    passcode = fields.Str(required=False, metadata={"description": "6-digit passcode"})
