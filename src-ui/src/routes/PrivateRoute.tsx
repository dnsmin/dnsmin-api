import {useEffect} from 'react';
import {Outlet, useLocation, useNavigate} from 'react-router-dom';
import {useAppDispatch, useAppSelector} from '@store/store';
import {setRedirectPath} from '@store/reducers/auth';

const PrivateRoute = () => {
    const dispatch = useAppDispatch();
    const location = useLocation();
    const navigate = useNavigate();
    const isLoggedIn = useAppSelector((state) => state.auth.currentUser);

    useEffect(() => {
        dispatch(setRedirectPath(location.pathname + location.search));
    }, [dispatch, location.pathname, location.search]);

    useEffect(() => {
        if (!isLoggedIn) {
            navigate('/user/login');
        }
    }, [navigate, isLoggedIn]);

    return <Outlet/>;
};

export default PrivateRoute;
