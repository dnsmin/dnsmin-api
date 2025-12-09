import * as React from "react";
import {Paper, Typography} from "@mui/material";

interface StatisticCardProps {
    label: string;
    value: any;
}

const StatisticCard: React.FC<StatisticCardProps> = ({label, value}) => {
    return (
        <>
            <Paper elevation={2} variant="outlined" sx={{width: '100%', padding: 2}}>
                <Typography variant="h4">{value}</Typography>
                <Typography variant="body1">{label}</Typography>
            </Paper>
        </>
    )
};

export default StatisticCard;