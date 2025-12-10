import {RefObject} from 'react';
import {GridGetRowsParams, GridGetRowsResponse, GridColDef} from '@mui/x-data-grid';
import {GridApiPro, GridDataSource} from '@mui/x-data-grid-pro';
import {
    IServiceCallback,
    IGridServiceProps,
    IRecord,
    IValidationErrorResponse,
    IValidationErrors
} from '@app/types/service';

export class ApiResourceService {
    protected apiResourceUrl: string;
    protected subscribers: Set<IServiceCallback> = new Set();
    protected _gridApiRef: RefObject<GridApiPro> | undefined = undefined;
    protected _gridDatasource: GridDataSource | undefined = undefined;
    protected _records: IRecord[] = [];
    protected _totalRecords: number = 0;
    protected _totalFilteredRecords: number = 0;

    constructor(apiResourceUrl: string) {
        this.apiResourceUrl = apiResourceUrl;
    }

    async getRecords(params: GridGetRowsParams): Promise<GridGetRowsResponse> {
        const response = await this.makeRequest(this.apiResourceUrl, params);

        const data = await response.json();

        this._records = data.records;
        this.emit(data.total, data.records.length);

        return {
            rows: data.records,
            rowCount: data.total,
        };
    }

    async getRecord(id: string): Promise<IRecord> {
        const response = await this.makeRequest(`${this.apiResourceUrl}/${id}`, undefined, 'GET');
        return await response.json();
    }

    async saveRecord(record: IRecord): Promise<boolean | IValidationErrors> {
        const requestUrl = record.id ? `${this.apiResourceUrl}/${record.id}` : `${this.apiResourceUrl}/create`;
        const response = await this.makeRequest(requestUrl, record, record.id ? 'PATCH' : 'POST');

        const data = await response.json();

        if (response.status >= 200 && response.status < 300) {
            this._gridApiRef?.current?.dataSource.cache.clear();
            await this._gridApiRef?.current?.dataSource.fetchRows();
            return true;
        }

        if (response.status === 422) {
            return this.extractValidationErrors(data);
        }

        return false;
    }

    getGridProps(columns: readonly GridColDef<any>[], gridApiRef: RefObject<GridApiPro> | undefined): IGridServiceProps {
        this._gridApiRef = gridApiRef!;
        return {
            columns: columns,
            apiRef: this._gridApiRef,
            dataSource: this.gridDatasource,
            pagination: true,
            pageSizeOptions: [5, 10, 25, 50, 100],
            sortingMode: 'server',
            filterMode: 'server',
            paginationMode: 'server',
            onStateChange: this.gridStateChangeHandler.bind(this),
            onDataSourceError: this.gridDataSourceErrorHandler.bind(this),
        }
    }

    get gridDatasource(): GridDataSource | undefined {
        if (this._gridDatasource !== undefined) {
            return this._gridDatasource;
        }

        this._gridDatasource = {
            getRows: this.getRecords.bind(this),
        };

        return this._gridDatasource;
    }

    get gridApiRef(): RefObject<GridApiPro> | undefined {
        return this._gridApiRef;
    }

    set gridApiRef(value: RefObject<GridApiPro>) {
        this._gridApiRef = value;
    }

    get records(): IRecord[] {
        return this._records;
    }

    get totalRecords(): number {
        return this._totalRecords;
    }

    get totalFilteredRecords(): number {
        return this._totalFilteredRecords;
    }

    onUsersStateChanged(callback: IServiceCallback): () => void {
        this.subscribers.add(callback);

        callback(this._totalRecords, this._totalFilteredRecords);

        return () => {
            this.subscribers.delete(callback);
        };
    }

    protected emit(totalRecords: number, filteredRecords: number) {
        this._totalRecords = totalRecords;
        this._totalFilteredRecords = filteredRecords;
        for (const cb of this.subscribers) cb(totalRecords, filteredRecords);
    }

    protected async makeRequest(url: string, payload: object | undefined = undefined, method: string = 'POST'): Promise<Response> {
        const params: RequestInit = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (typeof payload === 'object') {
            params.body = JSON.stringify(payload);
        }

        return await fetch(url, params);
    }

    protected extractValidationErrors(data: IValidationErrorResponse): IValidationErrors {
        const errors: IValidationErrors = {};

        if (data.detail && typeof data.detail === 'object' && data.detail.length) {
            for (const error of data.detail) {
                errors[error.loc[error.loc.length - 1]] = error.msg;
            }
        }

        return errors;
    }

    protected gridStateChangeHandler() {
        const totalRows = this._gridApiRef?.current?.getRowsCount();
        this.emit(this._totalRecords, totalRows || this._totalFilteredRecords);
    }

    protected gridDataSourceErrorHandler(): (error: any) => void {
        return (error: any) => {
            console.error('Grid Datasource Error:', error);
        }
    }
}
