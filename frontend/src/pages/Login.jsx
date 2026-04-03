import { useState } from "react";
import { loginUser } from "../api/auth";

export default function Login(){

  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");

  const handleLogin=async()=>{

    try{

      const res=await loginUser(
        username,
        password
      );

      const token=res.data.access_token;
      const role=res.data.role;
      const userId=res.data.user_id;

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

    }catch(e){

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