import * as React from 'react';
import {useNavigate} from 'react-router-dom';
import {Container, Box, Button} from '@mui/material';
import {NavItem} from '@app/types/nav';
import {getNavItem} from '@app/routes/nav';

interface NavigationProps {
    baseNavKey?: string;
}

const SubNavigation: React.FC<NavigationProps> = ({baseNavKey}) => {
    const [navItem, setNavItem] = React.useState<NavItem | boolean>(false);
    const [navItems, setNavItems] = React.useState<NavItem[]>([]);
    const navigate = useNavigate();

    const handleNavClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
        e.preventDefault();

        if (typeof navItem !== 'object') {
            return false;
        }

        const subNavItem: NavItem | boolean = getNavItem(baseNavKey!, e.currentTarget.dataset.key);

        if (typeof subNavItem !== 'object') {
            return false;
        }

        const path = `${navItem.path}${subNavItem.path}`;

        navigate(path);
        return true;
    };

    React.useEffect(() => {
        if (typeof baseNavKey !== 'string') {
            setNavItem(false);
            setNavItems([]);
            return;
        }

        const navItem: NavItem | boolean = getNavItem(baseNavKey);

        setNavItem(navItem);

        if (typeof navItem !== 'object' || !navItem.children) {
            setNavItems([]);
            return;
        }

        setNavItems(navItem.children);

    }, [baseNavKey]);

    return (
        <>
            <Container>
                <Box sx={{display: 'flex', justifyContent: 'left'}}>
                    {navItems?.map((ni, index) => (
                        <Button
                            key={index}
                            href="#"
                            data-key={ni.key}
                            onClick={handleNavClick}
                            className="headerNav"
                            sx={{my: 2, mx: {md: 1, lg: 2}, display: 'block'}}
                        >
                            {ni.label}
                        </Button>
                    ))}
                </Box>
            </Container>
        </>
    )
};

export default SubNavigation;