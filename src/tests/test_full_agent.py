import asyncio
import websockets
import json

async def test_bioagent():
    uri = "ws://localhost:8000/ws/test-client"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({
            "type": "analyze_file",
            "file_path": "SRR11140744_R1.fastq",
            "content": "analyze this fastq file using fastqc and provide quality metrics"
        }))
        result = await websocket.recv()
        print(json.dumps(json.loads(result), indent=2))

if __name__ == "__main__":
    asyncio.run(test_bioagent())
