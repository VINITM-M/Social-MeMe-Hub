import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const OtpVerify = () => {
    const navigate = useNavigate();
    const [otp, setOtp] = useState('');

    return (

        <div className="otp-card">
            <div className="main-otp">
                <div className="close">
                    <CloseIcon />

                </div>
                <div class="otp-group">

                    <div className='otp-description'> We shared the OTP on this Email Address : [EMAIL_ADDRESS]
                        <input type="text" maxlength="1" inputmode="numeric">
                            <input type="text" maxlength="1" inputmode="numeric">
                                <input type="text" maxlength="1" inputmode="numeric">
                                    <input type="text" maxlength="1" inputmode="numeric">
                                    </div>
                                    <div className="Otp-verification"> OTP Verification Page
                                    </div>

                                    <div className='digit-pin'>

                                    </div>

                                    <div className='resend-btn'> Resend OTP </div>
                                    <div className="verify OTP"> Verify </div>

                                </div>
                            </div>

                            )
    
}

                            export default OtpVerify;