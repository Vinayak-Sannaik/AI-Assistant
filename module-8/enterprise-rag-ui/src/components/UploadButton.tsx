interface Props {
  onUpload: (file: File) => void;
}

export default function UploadButton({
  onUpload,
}: Props) {
  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
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

      <div className="cursor-pointer bg-blue-600 text-white text-center p-3 rounded-lg hover:bg-blue-700">
        Upload Document
      </div>
    </label>
  );
}