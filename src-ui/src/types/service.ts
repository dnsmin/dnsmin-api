import {RefObject} from 'react';
import {GridColDef, GridEventListener, GridGetRowsError, GridUpdateRowError} from '@mui/x-data-grid';
import {GridApiPro, GridDataSource, GridFeatureMode} from '@mui/x-data-grid-pro';

export type ServiceCallback = (totalRecords: number, filteredRecords: number) => void;

export interface GridServiceProps {
    columns: readonly GridColDef<any>[],
    apiRef: RefObject<GridApiPro> | undefined,
    dataSource: GridDataSource | undefined,
    pagination: boolean,
    pageSizeOptions: number[],
    sortingMode: GridFeatureMode,
    filterMode: GridFeatureMode,
    paginationMode: GridFeatureMode,
    onStateChange: GridEventListener<'stateChange'>,
    onDataSourceError: (error: GridUpdateRowError | GridGetRowsError) => {},
}

export type IGridServiceProps = GridServiceProps;

export interface Record {
    id?: string;
}

export interface FieldError {
    loc: string[],
    msg: string,
    type: string,
}

export interface ValidationErrorResponse {
    detail: FieldError[],
}

export interface ValidationErrors {
    [key: string]: string | undefined;
}

export type IRecordFormMode = 'create' | 'update';
export type IServiceCallback = ServiceCallback;
export type IRecord = Record;
export type IFieldError = FieldError;
export type IValidationErrorResponse = ValidationErrorResponse;
export type IValidationErrors = ValidationErrors;