import os

class FileAnalysisService:
    def analyze_directory(self, directory: str):
        if not os.path.exists(directory):
            return {"error": "directory not found"}
        files = []
        for root, dirs, filenames in os.walk(directory):
            for f in filenames:
                files.append(os.path.join(root, f))
        return {
            "file_count": len(files),
            "files": files
        }
