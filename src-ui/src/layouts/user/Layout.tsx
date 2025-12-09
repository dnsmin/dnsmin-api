import {Outlet} from 'react-router-dom';
import {Container, Stack} from '@mui/material';
import Header from '@layouts/user/Header';
import Footer from '@layouts/user/Footer';

export const Layout = () => {
    return (
        <>
            <Container maxWidth={false} disableGutters>
                <Stack>
                    <Header/>
                    <Container maxWidth={false} disableGutters sx={{paddingX: 1, mb: '30px'}}>
                        <Outlet/>
                    </Container>
                    <Footer/>
                </Stack>
            </Container>
        </>
    )
}

export default Layout
