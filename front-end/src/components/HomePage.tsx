import '../styles/HomePage.css';
import AddIcon from '@mui/icons-material/Add';
import VpnKeyIcon from '@mui/icons-material/VpnKey';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';

const HomePage = () => {

    const navigate = useNavigate();

    return (
        <div className="home-page">
            <div className="left-cards">

                <div className="card" onClick={() => navigate('/create-newroom')}>
                    <div className="top-section">
                        <AddIcon className="icon" />
                    </div>
                    <div className="bottom-section">
                        <p className="text">CREATE ROOM</p>
                    </div>
                </div>

                <div className="card" onClick={() => navigate('/enter-room')}>
                    <div className="top-section">
                        <VpnKeyIcon className="icon" />
                    </div>
                    <div className="bottom-section">
                        <p className="text">ENTER CODE</p>
                    </div>
                </div>

            </div>

            <div className="right-card">
                <div className="top-section large">
                    <SearchIcon className="icon large-icon" />
                </div>
                <div className="bottom-section dark">
                    <p className="text">FIND GAME</p>
                </div>
            </div>

        </div>
    );
};

export default HomePage;
