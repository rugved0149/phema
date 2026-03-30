import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const uploadFile = async (file) => {

  const formData = new FormData();

  formData.append("file", file);

  const res = await api.post(
    "/phema/upload",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    }
  );

  return res.data;

};