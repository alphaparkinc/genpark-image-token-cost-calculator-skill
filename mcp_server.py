import sys
import json
from client import VisionTokenCostCalculator

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-image-token-cost-calculator-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_vision_tokens",
                        "description": "Calculates vision token consumption and USD cost for an image dimension",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "width": {"type": "integer"},
                                "height": {"type": "integer"},
                                "provider": {"type": "string", "enum": ["openai", "anthropic"], "default": "openai"},
                                "detail": {"type": "string", "enum": ["low", "high"], "default": "high"}
                            },
                            "required": ["width", "height"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "calculate_vision_tokens":
            w = args.get("width", 1024)
            h = args.get("height", 768)
            provider = args.get("provider", "openai")
            if provider == "anthropic":
                res = VisionTokenCostCalculator.calculate_anthropic_tokens(w, h)
            else:
                res = VisionTokenCostCalculator.calculate_openai_tokens(w, h, args.get("detail", "high"))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
            
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def run():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    run()
