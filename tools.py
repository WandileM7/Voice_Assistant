# Define the tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "play_song",
            "description": "Play a song on Spotify by name or URI",
            "parameters": {
                "type": "object",
                "properties": {
                    "song_name": {
                        "type": "string",
                        "description": "The name of the song to play"
                    },
                    "song_uri": {
                        "type": "string",
                        "description": "The Spotify URI of the song to play"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "open_application",
            "description": "Open an application",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to open"
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "close_application",
            "description": "Close an application",
            "parameters": {
                "type": "object",
                "properties": {
                    "app_name": {
                        "type": "string",
                        "description": "The name of the application to close"
                    }
                },
                "required": ["app_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_whatsapp_message",
            "description": "Send a WhatsApp message",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {"type": "string"},
                    "message": {"type": "string"}
                },
                "required": ["recipient", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "schedule",
            "description": "Fetch the user's schedule",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "social_media",
            "description": "Open a social media website",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The social media platform to open"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_event",
            "description": "Create a new event in the user's Google Calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "summary": {
                        "type": "string",
                        "description": "Title of the event"
                    },
                    "location": {
                        "type": "string",
                        "description": "Location of the event"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description of the event"
                    },
                    "start_time": {
                        "type": "string",
                        "description": "Start time of the event in ISO 8601 format (e.g., '2023-07-21T09:00:00')"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time of the event in ISO 8601 format (e.g., '2023-07-21T10:00:00')"
                    },
                    "attendees": {
                        "type": "array",
                        "items": {
                            "type": "string"
                        },
                        "description": "List of attendee email addresses"
                    }
                },
                "required": ["summary", "start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_emails",
            "description": "Read recent emails from the Gmail inbox",
            "parameters": {
                "type": "object",
                "properties": {
                    "num_emails": {
                        "type": "integer",
                        "description": "Number of recent emails to read"
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email using Gmail",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string"},
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["to", "subject", "body"]
            }
        }
    }
]

    