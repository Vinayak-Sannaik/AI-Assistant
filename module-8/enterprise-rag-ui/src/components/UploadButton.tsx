interface Props {
  onUpload: (file: File) => void;
  uploading?: boolean;
}

import { Loader2, Upload } from "lucide-react";

export default function UploadButton({ onUpload, uploading }: Props) {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];

    if (file) {
      onUpload(file);
    }
  };

  return (
    <label className="block">
      <input
        type="file"
        accept=".pdf,.docx,.txt,.md"
        className="hidden"
        onChange={handleChange}
      />

      <div
        className={`flex items-center justify-center gap-2 text-white text-center p-3 rounded-lg ${
          uploading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 cursor-pointer"
        }`}
      >
        {uploading ? (
          <>
            <Loader2 size={18} className="animate-spin" />
            <span>Uploading...</span>
          </>
        ) : (
          <>
            <Upload size={18} />
            <span>Upload Document</span>
          </>
        )}
      </div>
    </label>
  );
}
