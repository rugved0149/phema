import axios from "axios";

/* BASE API CLIENT */

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000"
});


/* AUTO ATTACH JWT TOKEN */

api.interceptors.request.use(

  (config) => {

    const token =
      localStorage.getItem("token");

    if (token) {

      config.headers.Authorization =
        `Bearer ${token}`;

    }

    return config;

  },

  (error) => Promise.reject(error)

);


/* FILE UPLOAD */

export const uploadFile = async (file) => {

  const formData = new FormData();

  formData.append(
    "file",
    file
  );

  const res = await api.post(

    "/phema/upload",

    formData,

    {
      headers: {
        "Content-Type":
          "multipart/form-data"
      }
    }

  );

  return res.data;

};


/* AUTH API CALLS */

export const registerUser = async (
  email,
  username,
  password
) => {

  const res = await api.post(
    "/auth/register",
    null,
    {
      params: {
        email,
        username,
        password
      }
    }
  );

  return res.data;

};


export const verifyOTP = async (
  email,
  username,
  password,
  otp
) => {

  const res = await api.post(
    "/auth/verify",
    null,
    {
      params: {
        email,
        username,
        password,
        otp
      }
    }
  );

  return res.data;

};


export const loginUser = async (
  username,
  password
) => {

  const res = await api.post(
    "/auth/login",
    null,
    {
      params: {
        username,
        password
      }
    }
  );

  return res.data;

};


/* ALSO EXPORT DEFAULT */

export default api;