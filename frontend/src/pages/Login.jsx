import { useState } from "react";
import { loginUser } from "../api/client";

export default function Login(){

  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");

  const handleLogin=async()=>{

    try{

      const res=await loginUser(
        username,
        password
      );

      const token=res.access_token;
      const role=res.role;
      const userId=res.user_id;

      localStorage.setItem(
        "token",
        token
      );

      localStorage.setItem(
        "role",
        role
      );

      localStorage.setItem(
        "user_id",
        userId
      );

      if(role==="admin"){

        window.location="/admin";

      }else{

        window.location="/user";

      }

    }
    catch(e){

      console.error(e);

      alert("Login failed");

    }

  };

  return(

    <div>

      <h2>Login</h2>

      <input
        placeholder="Username"
        onChange={(e)=>
          setUsername(e.target.value)
        }
      />

      <input
        type="password"
        placeholder="Password"
        onChange={(e)=>
          setPassword(e.target.value)
        }
      />

      <button
        onClick={handleLogin}
      >
        Login
      </button>

    </div>

  );

}