import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

const OtpVerify = () => {

  const navigate = useNavigate();

  const [otp, setOtp] = useState("");
  const [resendCount, setResendCount] = useState(0);

 // Function to resend the OTP to the user's email 
  const resendOtp = async () => {

    if (resendCount >= 3) {
      alert(
        "You have exceeded the maximum number of OTP resend attempts."
      ); 
      return;
    }
    try {

      const payload = {
        email_id: localStorage.getItem("email_id")
      };

      await axios.post(
        `${process.env.REACT_APP_API_URL}/otp`,
        payload
      );

      setResendCount(prev => prev + 1);
      alert("OTP Sent Successfully");
    }
    catch (error) {
      alert("Unable to send OTP");
    }
  };
  // Function to verify the OTP entered by the user 
  const verifyOtp = async () => {

    try {
      const payload = {
        email_id: localStorage.getItem("email_id"),
        otp: otp
      };
      const response =await axios.post(`${process.env.REACT_APP_API_URL}/verify-otp`,payload);
      alert(response.data.message);
    }
    catch (error) {

      const message = error.response?.data?.detail;
      if (message ==="Maximum OTP attempts exceeded") {
        alert("Maximum OTP attempts exceeded. Request a new OTP.");
      }
      else if (message === "OTP Expired") {
        alert("OTP Expired");
      }
      else if (message === "No OTP request found for this email") {

        alert("No OTP request found.");

      }
      else if (message ==="Invalid OTP") {
        alert("Invalid OTP");
      }
      else {
        alert("Server Error");
      }
    }
  };

  return (

    <div className="otp-verify-container">

      <div className="otp-verify-box">

        <h2>OTP Verification</h2>

        <input
          type="text"
          value={otp}
          onChange={(e) =>
            setOtp(e.target.value)
          }
          placeholder="Enter OTP"
        />

        <button onClick={verifyOtp}>
          Verify OTP
        </button>

        <button onClick={resendOtp}>
          Resend OTP
        </button>

      </div>

    </div>
  );
};

export default OtpVerify;