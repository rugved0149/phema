import axios from "axios";

/* BASE API CLIENT */

export const api=axios.create({

  baseURL:"http://127.0.0.1:8000"

});


/* AUTO ATTACH JWT TOKEN */

api.interceptors.request.use(

  (config)=>{

    const token=
      localStorage.getItem("token");

    if(token){

      config.headers.Authorization=
        `Bearer ${token}`;

    }

    return config;

  },

  (error)=>Promise.reject(error)

);


/* AUTO REFRESH TOKEN */

api.interceptors.response.use(

  (response)=>response,

  async(error)=>{

    const originalRequest=
      error.config;

    /* Ignore refresh/login failures */

    if(
      originalRequest?.url?.includes("/auth/login") ||
      originalRequest?.url?.includes("/auth/refresh")
    ){

      return Promise.reject(error);

    }

    if(
      error.response &&
      error.response.status===401 &&
      !originalRequest._retry
    ){

      originalRequest._retry=true;

      const refresh=
        localStorage.getItem("refresh");

      /* No refresh token → logout */

      if(!refresh){

        localStorage.clear();

        window.location="/login";

        return Promise.reject(error);

      }

      try{

        const res=await axios.post(

          "http://127.0.0.1:8000/auth/refresh",

          null,

          {

            params:{
              refresh_token:refresh
            }

          }

        );

        const newAccess=
          res.data.access_token;

        if(!newAccess){

          throw new Error("No access token");

        }

        localStorage.setItem(
          "token",
          newAccess
        );

        /* Update header */

        originalRequest.headers.Authorization=
          `Bearer ${newAccess}`;

        return api(originalRequest);

      }

      catch(refreshError){

        /* Hard logout */

        localStorage.clear();

        window.location="/login";

        return Promise.reject(refreshError);

      }

    }

    return Promise.reject(error);

  }

);


/* FILE UPLOAD */

export const uploadFile=async(file)=>{

  const formData=new FormData();

  formData.append(
    "file",
    file
  );

  const res=await api.post(

    "/phema/upload",

    formData,

    {

      headers:{
        "Content-Type":
          "multipart/form-data"
      }

    }

  );

  return res.data;

};


/* AUTH API */

export const registerUser=async(
  email,
  username,
  password
)=>{

  const res=await api.post(

    "/auth/register",

    null,

    {

      params:{
        email,
        username,
        password
      }

    }

  );

  return res.data;

};


export const verifyOTP=async(
  email,
  username,
  password,
  otp
)=>{

  const res=await api.post(

    "/auth/verify",

    null,

    {

      params:{
        email,
        username,
        password,
        otp
      }

    }

  );

  return res.data;

};


export const loginUser=async(
  username,
  password
)=>{

  const res=await api.post(

    "/auth/login",

    null,

    {

      params:{
        username,
        password
      }

    }

  );

  const access=res.data.access_token;
  const refresh=res.data.refresh_token;
  const userId=res.data.user_id;
  const role=res.data.role;

  if(access){

    localStorage.setItem(
      "token",
      access
    );

  }

  if(refresh){

    localStorage.setItem(
      "refresh",
      refresh
    );

  }

  if(userId){

    localStorage.setItem(
      "user_id",
      userId
    );

  }

  if(role){

    localStorage.setItem(
      "role",
      role
    );

  }

  return res.data;

};


/* DEFAULT EXPORT */

export default api;