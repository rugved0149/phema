import { useState } from "react";
import { verifyOTP } from "../api/auth";

export default function Verify(){

  const [otp,setOtp]=useState("");

  const handleVerify=async()=>{

    const email=
      localStorage.getItem("reg_email");

    const username=
      localStorage.getItem("reg_username");

    const password=
      localStorage.getItem("reg_password");

    await verifyOTP(
      email,
      username,
      password,
      otp
    );

    window.location="/login";
  };

  return(

    <div>

      <h2>Verify OTP</h2>

      <input
        placeholder="Enter OTP"
        onChange={(e)=>
          setOtp(e.target.value)
        }
      />

      <button
        onClick={handleVerify}
      >
        Verify
      </button>

    </div>

  );
}