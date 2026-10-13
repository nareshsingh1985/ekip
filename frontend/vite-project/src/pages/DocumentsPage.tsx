import FileUploader from "../components/FileUploader";
import UploadHistory from "../components/UploadHistory";
import DocumentRepository from "../components/DocumentRepository";

export default function DocumentsPage() {

  return (
    <>
      <FileUploader />
      <UploadHistory />
      <DocumentRepository />
    </>
  );
}
