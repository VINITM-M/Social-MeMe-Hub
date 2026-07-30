import React, { useState } from "react";
import "../styles/login_page.css";
import axios from "axios";
import CloseIcon from '@mui/icons-material/Close';


const LoginPage = () => {
    const [activeTab, setActiveTab] = useState("login");

    const [first_name, setfirst_name] = useState("");
    const [last_name, setlast_name] = useState("");
    const [email_id, setemail_id] = useState("");
    const [password, setpassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [showPopup, setShowPopup] = useState(false);
    const [userDetails, setUserDetails] = useState<any>(null);

    const handleLogin = async () => {

        const payload = {
            email_id: email_id,
            password: password
        };
        console.log("Login Payload:", payload);
        try {
            const response = await axios.post('http://127.0.0.1:8000/login', payload);
            console.log("Login Response:", response.data);
            // show user details in a popup instead of navigating
            setUserDetails(response.data);
            setShowPopup(true);
            
        } catch (error) {
            console.warn("Backend not available:", error);
        }
    };

    const popClose = async () => {
        setShowPopup(false);
        setUserDetails(null);
    }

    const handleSignup = async () => {

        const payload = {
            first_name: first_name,
            last_name: last_name,
            email_id: email_id,
            password: password
        };
        console.log("Signup Payload:", payload);
        try {
            const response = await axios.post('http://127.0.0.1:8000/signup', payload);
            console.log("Signup Response:", response.data);

            if(response.data.is_registered === false){
                alert("User already exists. Please login.");
            }else {
                alert("User registered successfully. Please login.");
            }

        } catch (error) {
            console.warn("Backend not available:", error);
        }

    }

    return (
        <div className="main-login-box">
            <div className="login-card">
                {/* Popup modal for showing user details */}
                {showPopup && userDetails && (
                    <div className="modal-backdrop">
                        <div className="modal">
                            <div className="modal-close" onClick={popClose}><CloseIcon /></div>
                            <h3>User Details</h3>
                            <div className="user-detail-row"><strong>Name:</strong> {userDetails.first_name || userDetails.name || "-"} {userDetails.last_name || ""}</div>
                            <div className="user-detail-row"><strong>Email:</strong> {userDetails.email_id || userDetails.email || "-"}</div>
                            {userDetails.room && <div className="user-detail-row"><strong>Room:</strong> {userDetails.room}</div>}
                            <div style={{marginTop:16}}>
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