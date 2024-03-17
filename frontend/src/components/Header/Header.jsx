import notifications from '/notification-bell.png';
import avatar from '/user-avatar.png';


const Header = () => {
    return (
        <header>
            <nav>
                <a href="#">QUICKER</a>
                <div>
                    <img src={notifications} alt="notifications"/>
                    <div>
                        <img src={avatar} alt="user-avatar"/>
                        <div>
                            <a href="#">Profile</a>
                            <a href="#">Settings</a>
                            <a href="#">Log Out</a>
                        </div>
                    </div>
                </div>
            </nav>
        </header>
    );
};

export default Header;
