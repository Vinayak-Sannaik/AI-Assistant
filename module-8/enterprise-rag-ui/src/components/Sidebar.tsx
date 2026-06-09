import { useState, useEffect } from "react";
import UploadButton from "./UploadButton";
import {
  uploadDocument,
  getKnowledgeBase,
  deleteDocument,
} from "../api/ragApi";

export default function Sidebar() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [uploading, setUploading] = useState(false);

  const [totalChunks, setTotalChunks] = useState(0);

  const loadKnowledgeBase = async () => {
    try {
      setUploading(true);
      const data = await getKnowledgeBase();
      setDocuments(
        data.documents.map((doc: { filename: string }) => doc.filename),
      );

      setTotalChunks(data.total_chunks);
    } catch (error) {
      console.error(error);
    } finally {
      setUploading(false);
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

  const handleDelete = async (filename: string) => {
    const confirmed = window.confirm(`Delete ${filename}?`);

    if (!confirmed) return;

    try {
      await deleteDocument(filename);

      await loadKnowledgeBase();
    } catch (error) {
      console.error(error);

      alert("Delete failed");
    }
  };
  return (
    <div className="w-72 bg-white border-r p-4">
      <h2 className="text-xl font-bold mb-4">Knowledge Base</h2>

      <UploadButton onUpload={handleUpload} uploading={uploading} />

      <div>
        <h3 className="font-semibold mb-2">Documents</h3>

        <ul className="space-y-2 text-sm">
          {documents.map((doc) => (
            <li key={doc} className="group flex items-center justify-between">
              <span className="truncate" title={doc}>
                📄 {doc}
              </span>

              <button
                onClick={() => handleDelete(doc)}
                className="opacity-0 group-hover:opacity-100 text-red-500 text-xs"
              >
                ✕
              </button>
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
