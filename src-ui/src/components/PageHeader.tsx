import * as React from "react";
import {Box, Typography} from "@mui/material";

interface PageHeaderProps {
    title: string;
}

const PageHeader: React.FC<PageHeaderProps> = ({title}) => {
    return (
        <>
            <Box sx={{display: 'flex', justifyContent: 'space-between', mb: 2}}>
                <Typography variant="h1" className="pageHeader">{title}</Typography>
            </Box>
        </>
    )
};

export default PageHeader;