import {useEffect} from 'react';
import {Outlet, useNavigate} from 'react-router-dom';
import {useAppSelector} from '@store/store';

const PublicRoute = () => {
    const navigate = useNavigate();
    const isLoggedIn = useAppSelector((state) => state.auth.currentUser);
    const redirectPath = useAppSelector((state) => state.auth.redirectPath);

    useEffect(() => {
        if (isLoggedIn) {
            console.warn('Redirect Path:', redirectPath);
            navigate(redirectPath || '/');

        }
    }, [navigate, isLoggedIn, redirectPath]);

    return <Outlet/>;
};

export default PublicRoute;
