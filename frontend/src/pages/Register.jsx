import { useState } from "react";
import { registerUser } from "../api/auth";

export default function Register(){

  const [email,setEmail]=useState("");
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");

  const handleRegister=async()=>{

    await registerUser(
      email,
      username,
      password
    );

    localStorage.setItem(
      "reg_email",
      email
    );

    localStorage.setItem(
      "reg_username",
      username
    );

    localStorage.setItem(
      "reg_password",
      password
    );

    window.location="/verify";

  };

  return(

    <div>

      <h2>Register</h2>

      <input
        placeholder="Email"
        onChange={(e)=>
          setEmail(e.target.value)
        }
      />

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
        onClick={handleRegister}
      >
        Register
      </button>

    </div>

  );
}