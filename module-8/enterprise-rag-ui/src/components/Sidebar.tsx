import { useState, useEffect } from "react";
import UploadButton from "./UploadButton";
import { uploadDocument, getKnowledgeBase } from "../api/ragApi";

export default function Sidebar() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  const [totalChunks, setTotalChunks] = useState(0);

  const loadKnowledgeBase = async () => {
    try {
      setUploading(true)
      const data = await getKnowledgeBase();
      setDocuments(
        data.documents.map((doc: { filename: string }) => doc.filename),
      );

      setTotalChunks(data.total_chunks);
    } catch (error) {
      console.error(error);
    } finally {
      setUploading(false)
    }
  };

  useEffect(() => {
    void loadKnowledgeBase();
  }, []);

  const handleUpload = async (file: File) => {
    try {
      const result = await uploadDocument(file);

      console.log(result);

      await loadKnowledgeBase();

      // alert(result.message);
    } catch (error) {
      console.error(error);

      alert("Upload failed");
    }
  };
  return (
    <div className="w-72 bg-white border-r p-4">
      <h2 className="text-xl font-bold mb-4">Knowledge Base</h2>

      <UploadButton onUpload={handleUpload} uploading={uploading}/>

      <div>
        <h3 className="font-semibold mb-2">Documents</h3>

        <ul className="space-y-2 text-sm">
          {documents.map((doc) => (
            <li key={doc} className="truncate cursor-default" title={doc}>
              {doc}
            </li>
          ))}
        </ul>
      </div>

      <div className="mt-8">
        <p>Total Documents: {documents.length}</p>
        <p>Total Chunks: {totalChunks}</p>
      </div>
    </div>
  );
}
