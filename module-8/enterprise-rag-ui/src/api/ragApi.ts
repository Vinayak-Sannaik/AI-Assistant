import axios from "axios";
import type { AskResponse } from "../types";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});


export const askQuestion = async (
  question: string
) => {
  const response = await api.post(
    "/ask",
    {
      question,
    }
  );

  return response.data;
};


export const uploadDocument = async (
  file: File
) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post(
  "/upload",
  formData
);

  return response.data;
};

export const getKnowledgeBase = async () => {
  const response = await api.get(
    "/knowledge-base"
  );

  return response.data;
};


export const deleteDocument = async (
  filename: string,
) => {
  const response = await fetch(
    `${import.meta.env.VITE_API_URL}/knowledge-base/${encodeURIComponent(filename)}`,
    {
      method: "DELETE",
    },
  );

  if (!response.ok) {
    throw new Error(
      "Failed to delete document",
    );
  }

  return response.json();
};