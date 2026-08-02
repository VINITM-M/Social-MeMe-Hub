import axios from "axios";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import '../styles/otp_verify.css'
import CloseIcon from "@mui/icons-material/Close";

const OtpVerify = () => {

  const navigate = useNavigate();
  const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  const [otp, setOtp] = useState("");
  const [resendCount, setResendCount] = useState(0);

  const handleClose = () => {
    navigate("/home");
  };

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

      const response = await axios.post(
        `${API_URL}/otp`,
        payload
      );

      setResendCount(prev => prev + 1);
      if (response.data?.otp) {
        localStorage.setItem("dev_otp", response.data.otp);
        alert(`OTP Sent Successfully. Test OTP: ${response.data.otp}`);
      } else {
        alert("OTP Sent Successfully");
      }
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
      const response = await axios.post(`${API_URL}/verify-otp`, payload);
      alert(response.data.message);
      navigate('/home')
    }
    catch (error) {

      const axiosError = error as { response?: { data?: { detail?: string } } };

      const message = axiosError.response?.data?.detail;
      if (message === "Maximum OTP attempts exceeded") {
        alert("Maximum OTP attempts exceeded. Request a new OTP.");
      }
      else if (message === "OTP Expired") {
        alert("OTP Expired");
      }
      else if (message === "No OTP request found for this email") {

        alert("No OTP request found.");

      }
      else if (message === "Invalid OTP") {
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
        <div className="closeIcon" onClick={handleClose}>
          <CloseIcon />
        </div>
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