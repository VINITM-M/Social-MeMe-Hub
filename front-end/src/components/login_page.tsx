import React, { useState } from "react";
import "../styles/login_page.css";
import axios from "axios";
import CloseIcon from '@mui/icons-material/Close';
import { useNavigate } from "react-router-dom";

interface LoginPageProps {
    onClose?: () => void;
}

const LoginPage: React.FC<LoginPageProps> = ({ onClose }) => {
    const navigate = useNavigate();
    const [activeTab, setActiveTab] = useState("login");

    const [first_name, setfirst_name] = useState("");
    const [last_name, setlast_name] = useState("");
    const [email_id, setemail_id] = useState("");vh
    const [password, setpassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPopup, setShowPopup] = useState(false);
    const [userDetails, setUserDetails] = useState<any>(null);
    const [errorMessage, setErrorMessage] = useState(""); 
    
    const API_URL = process.env.REACT_APP_API_URL

    //otp verify logic 
    const otp = async () => {

        const payload = {
            email_id: email_id
        }
        try {
            const response = await axios.post(`${API_URL}/otp`, payload)
            console.log("OTP Response:", response.data)

        } catch (error) {
            console.warn("Backend not available:", error);
        }
    }
    // Login details validation function 
    const handleLogin = async () => {

        const payload = {
            email_id: email_id,
            password: password
        };
        try {
            const response = await axios.post(`${API_URL}/login`, payload);

            if (response.data?.status == 200) {

                await otpverify();

                navigate("/otp_verify");

                return;
            }

        } catch (error) {

            if (error.response?.status === 401) {
                setErrorMessage("Invalid Password");
            }
            else if (error.response?.status === 404) {
                setErrorMessage("User not found");
            }
            else {
                setErrorMessage("Server error. Please try again later.");
            }
        }
    };
    // Signup details validation function 
    const handleSignup = async () => {

        const payload = {
            first_name: first_name,
            last_name: last_name,
            email_id: email_id,
            password: password
        };

        try {
            const response = await axios.post(`${API_URL}/signup`, payload); 

            if (response.data?.message === "User registered successfully") {

                await otp();
                navigate("/otp_verify");

                return;
            }
        } catch (error) {
            if(error.response?.status == 400){
                alert("User already exists, please Login"); 
            }
            else{
                console.warn("Backend not available:", error);
            }
        }

    }
    const handleClose = () => {
        if (onClose) {
            onClose();
        } else {
            navigate(-1);
        }
    };

    const popClose = async () => {
        setShowPopup(false);
        setUserDetails(null);
    }
    return (
        <div className="main-login-box" onClick={(e) => { if (e.target === e.currentTarget) handleClose(); }}>
            <div className="login-card">
                <div className="closeIcon" onClick={handleClose} title="Close">
                    <CloseIcon />
                </div>
                {/* Popup modal for showing user details */}
                {showPopup && userDetails && (
                    <div className="modal-backdrop">
                        <div className="modal">
                            <div className="modal-close" onClick={popClose}><CloseIcon /></div>
                            <h3>User Details</h3>
                            <div className="user-detail-row"><strong>Name:</strong> {userDetails.first_name || userDetails.name || "-"} {userDetails.last_name || ""}</div>
                            <div className="user-detail-row"><strong>Email:</strong> {userDetails.email_id || userDetails.email || "-"}</div>
                            {userDetails.room && <div className="user-detail-row"><strong>Room:</strong> {userDetails.room}</div>}
                            <div style={{ marginTop: 16 }}>
                                <button className="login-button" onClick={popClose}>Close</button>
                            </div>
                        </div>
                    </div>
                )}
                {/* Toggle Buttons */}
                <div className="switch-container">
                    <button
                        className={activeTab === "login" ? "active-tab" : ""}
                        onClick={() => setActiveTab("login")}
                    >
                        Login
                    </button>

                    <button
                        className={activeTab === "signup" ? "active-tab" : ""}
                        onClick={() => setActiveTab("signup")}
                    >
                        Signup
                    </button>
                </div>

                {/* LOGIN FORM */}
                {activeTab === "login" && (
                    <>
                        <div className="email-div">
                            <div className="email-text">Email Address</div>
                            <input
                                className="email-input"
                                type="email"
                                placeholder="Enter your email address"
                                value={email_id}
                                onChange={(e) => setemail_id(e.target.value)}
                            />
                        </div>

                        <div className="password-div">
                            <div className="password-text">
                                Enter Password
                            </div>
                            <input
                                className="password-input"
                                type="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) => setpassword(e.target.value)}
                            />
                        </div>

                        <div className="remember-me-forgot-password-div">
                            <div className="remember-me-div">
                                <input
                                    className="remember-me-checkbox"
                                    type="checkbox"
                                />
                                <label>Remember me</label>
                            </div>

                            <div className="forgot-password-div">
                                <label>Forgot Password?</label>
                            </div>
                        </div>

                        <div className="login-button-div" onClick={handleLogin}>
                            <button className="login-button" >
                                Login
                            </button>
                        </div>

                        <div className="sign-up-div">
                            <p>
                                Don't have an account?{" "}
                                <b
                                    style={{ cursor: "pointer" }}
                                    onClick={() => setActiveTab("signup")}
                                >
                                    Sign up
                                </b>
                            </p>
                        </div>
                    </>
                )}

                {/* SIGNUP FORM */}
                {activeTab === "signup" && (
                    <>
                        <div className="firstName-div">
                            <div className="firstName-text">
                                Enter Your First Name
                            </div>
                            <input
                                className="firstName-input"
                                type="text"
                                placeholder="Enter your first name"
                                value={first_name}
                                onChange={(e) =>
                                    setfirst_name(e.target.value)
                                }
                            />
                        </div>

                        <div className="lastName-div">
                            <div className="lastName-text">
                                Enter Your Last Name
                            </div>
                            <input
                                className="lastName-input"
                                type="text"
                                placeholder="Enter your last name"
                                value={last_name}
                                onChange={(e) =>
                                    setlast_name(e.target.value)
                                }
                            />
                        </div>

                        <div className="email-div">
                            <div className="email-text">
                                Enter Your Email Address
                            </div>
                            <input
                                className="email-input"
                                type="email"
                                placeholder="Enter your email address or phone number"
                                value={email_id}
                                onChange={(e) =>
                                    setemail_id(e.target.value)
                                }
                            />
                        </div>
                        <div className="password-div">
                            <div className="password-text">
                                Enter Password
                            </div>
                            <input
                                className="password-input"
                                type="password"
                                placeholder="Enter your password"
                                value={password}
                                onChange={(e) =>
                                    setpassword(e.target.value)
                                }
                            />
                        </div>

                        <div className="confirmPassword-div">
                            <div className="password-text">
                                Confirm Password
                            </div>

                            <input
                                className="confirmPassword-input"
                                type="password"
                                placeholder="Confirm your password"
                                value={confirmPassword}
                                onChange={(e) => setConfirmPassword(e.target.value)}
                            />

                            {confirmPassword &&
                                password !== confirmPassword && (
                                    <div className="password-mismatch">
                                        Passwords do not match
                                    </div>
                                )}
                        </div>

                        <div className="signup-created">
                            <button className="account-created-button" onClick={handleSignup}>
                                Sign Up
                            </button>
                        </div>

                        <div className="already-have-account">
                            <p>
                                Already have an account?{" "}
                                <b
                                    style={{ cursor: "pointer" }}
                                    onClick={() => setActiveTab("login")}
                                >
                                    Log-In Or
                                </b>
                            </p>
                        </div>
                    </>
                )}
            </div>
        </div>
    );
};

export default LoginPage;