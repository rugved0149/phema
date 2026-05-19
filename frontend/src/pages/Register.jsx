import { useState } from "react";
import { registerUser } from "../api/auth";

export default function Register(){

  const [email,setEmail]=useState("");
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");

  const [error,setError]=useState("");

  const handleRegister=async()=>{

    try{

      const res=await registerUser(
        email,
        username,
        password
      );

      const data=res.data;

      if(data.status==="weak_password"){

        setError(
          data.message ||
          "Weak password"
        );

        return;
      }

      if(data.status==="user_exists"){

        setError(
          "User already exists"
        );

        return;
      }

      if(data.status==="otp_sent"){

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

      }

    }
    catch(e){

      setError(
        "Registration failed"
      );

    }

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

      {/* ERROR DISPLAY */}

      {error && (

        <div
          style={{
            color:"red",
            marginTop:"8px"
          }}
        >
          {error}
        </div>

      )}

      <button
        onClick={handleRegister}
      >
        Register
      </button>

    </div>

  );
}