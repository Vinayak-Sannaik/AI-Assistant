import { useState } from "react";
import UploadButton from "./UploadButton";

export default function Sidebar() {
  const [documents, setDocuments] = useState<string[]>([
    "chromadb.md",
    "enterprise-rag.pdf",
  ]);

  const handleUpload = async (file: File) => {
    alert(`Uploaded ${file.name}`);
    setDocuments((prev) => [...prev, file.name]);
  };
  return (
    <div className="w-72 bg-white border-r p-4">
      <h2 className="text-xl font-bold mb-4">Knowledge Base</h2>

      <UploadButton onUpload={handleUpload} />

      <div>
        <h3 className="font-semibold mb-2">Documents</h3>

        <ul className="space-y-2 text-sm">
          {documents.map((doc) => (
            <li key={doc}>{doc}</li>
          ))}
        </ul>
      </div>

      <div className="mt-8">
        <p>Total Documents: {documents.length}</p>
        <p>Total Chunks: 127</p>
      </div>
    </div>
  );
}
