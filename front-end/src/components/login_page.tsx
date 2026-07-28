import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../styles/login_page.css';

const login_page = () => {

    const [first_name, setfirst_name] = useState('');
    const [last_name, setlast_name] = useState('');
    const [email_id, setemail_id] = useState('');
    const [phone_number, setphone_number] = useState('');
    const [password, setpassword] = useState('');
    const [dob, setdob] = useState('');

    const navigate = useNavigate();

    return (
        <div className='main-login-box'>
            <div className='login-card'>
                <div className='email-div'>
                    <div className='email-text'> Email address </div>
                    <input className='email-input' type="email" placeholder='Enter your enail address' value={email_id} onChange={(e) => setemail_id(e.target.value)} />
                </div>
            </div>
        </div>
    )
}; export default login_page 