import * as React from "react";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {Button, Grid} from "@mui/material";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import {
    DataGridPro,
    GridFilterModel,
    GridSortModel,
    GridPaginationModel,
    GridLogicOperator,
    GridColDef,
    GridActionsCellItem,
} from "@mui/x-data-grid-pro";
import {useUsers} from "@app/api/hooks/auth/users";
import PageHeader from "@components/PageHeader";
import StatisticCard from "@components/cards/StatisticCard";
import UserFormDialog from "@components/forms/UserFormDialog";


interface ViewProps {
    baseUrl: string;
    multiTenant?: boolean;
}

const Page = ({baseUrl, multiTenant = true}: ViewProps) => {
    const navigate = useNavigate();

    const [filterModel, setFilterModel] = useState<GridFilterModel>({
        items: [],
        quickFilterValues: [],
        logicOperator: GridLogicOperator.And,
    });

    const [sortModel, setSortModel] = useState<GridSortModel>([]);

    const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({page: 0, pageSize: 25});

    const {data, isLoading} = useUsers({filterModel, sortModel, paginationModel});

    const isFilteringActive = React.useMemo(() => {
        return filterModel.items.length > 0 || (filterModel.quickFilterValues?.length ?? 0) > 0;
    }, [filterModel]);

    const openCreate = () => {
        navigate(`${baseUrl}/create`);
    };

    const openUpdate = (id: string) => {
        navigate(`${baseUrl}/${id}/update`);
    };

    const openDelete = (id: string) => {
        navigate(`${baseUrl}/${id}/delete`);
    };

    const columns: readonly GridColDef<any>[] = [
        {field: 'id', headerName: 'User ID', width: 300},
        ...(multiTenant ? [{field: 'tenantId', headerName: 'Tenant ID', width: 300}] : []),
        {field: 'username', headerName: 'Username', width: 150},
        {field: 'email', headerName: 'Email', width: 200},
        {field: 'phoneNumber', headerName: 'Phone Number', width: 150},
        {field: 'status', headerName: 'Status', width: 100},
        {field: 'createdAt', headerName: 'Created', width: 175},
        {field: 'updatedAt', headerName: 'Updated', width: 175},
        {field: 'authenticatedAt', headerName: 'Last Login', width: 175},
        {
            field: 'actions',
            type: 'actions',
            headerName: 'Actions',
            width: 100,
            getActions: (params) => [
                <GridActionsCellItem
                    key="edit"
                    icon={<EditIcon/>}
                    label="Edit"
                    onClick={() => openUpdate(params.row.id)}
                    showInMenu
                />,
                <GridActionsCellItem
                    key="delete"
                    icon={<DeleteIcon/>}
                    label="Delete"
                    onClick={() => openDelete(params.row.id)}
                    showInMenu
                />,
            ],
        },
    ];

    return (
        <>
            <PageHeader title={'User Management'}/>
            <Grid container justifyContent="space-between">
                <Grid size={{sm: 12, md: 6, lg: 4}} paddingY={2}>
                    <Grid container spacing={2}>
                        <Grid size={{sm: 12, md: 6}}>
                            <StatisticCard label="Total Users" value={data?.total}/>
                        </Grid>
                        {isFilteringActive && (
                            <Grid size={{sm: 12, md: 6}}>
                                <StatisticCard label="Total Results" value={data?.records.length}/>
                            </Grid>
                        )}
                    </Grid>
                </Grid>
                <Grid size={{sm: 12, md: 3, lg: 2}} paddingY={2} display="flex" justifyContent="flex-end"
                      alignItems="flex-end">
                    <Button variant="contained" onClick={() => openCreate()}>Create User</Button>
                </Grid>
                <Grid size={12}>
                    <DataGridPro
                        autoHeight
                        loading={isLoading}
                        columns={columns}
                        rows={data?.records ?? []}
                        getRowId={(row) => row.id}
                        rowCount={data?.total ?? 0}
                        filterMode="server"
                        sortingMode="server"
                        paginationMode="server"
                        pagination={true}
                        pageSizeOptions={[5, 10, 25, 50, 100]}
                        filterModel={filterModel}
                        sortModel={sortModel}
                        paginationModel={paginationModel}
                        onFilterModelChange={(model) => setFilterModel(model)}
                        onSortModelChange={(model) => setSortModel(model)}
                        onPaginationModelChange={(model) => setPaginationModel(model)}
                        initialState={{
                            pinnedColumns: {
                                right: ['actions'],
                            },
                        }}
                    />
                </Grid>
            </Grid>
            <UserFormDialog basePath={baseUrl}/>
        </>
    );
};

export default Page;
