import {Outlet} from 'react-router-dom';
import {Container} from '@mui/material';

export const Layout = () => {
    return (
        <>
            <Container sx={{display: 'flex', minHeight: '100vh', justifyContent: 'center', alignItems: 'center'}}>
                <Outlet/>
            </Container>
        </>
    )
}

export default Layout
