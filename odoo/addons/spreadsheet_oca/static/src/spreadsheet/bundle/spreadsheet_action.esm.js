/** @odoo-module **/

import PivotDataSource from "@spreadsheet/pivot/pivot_data_source";
import {SpreadsheetControlPanel} from "./spreadsheet_controlpanel.esm";
import {SpreadsheetRenderer} from "./spreadsheet_renderer.esm";
import {registry} from "@web/core/registry";
import spreadsheet from "@spreadsheet/o_spreadsheet/o_spreadsheet_extended";
import {useService} from "@web/core/utils/hooks";

const uuidGenerator = new spreadsheet.helpers.UuidGenerator();
const actionRegistry = registry.category("actions");
const {Component, onMounted, onWillStart, useSubEnv} = owl;

export class ActionSpreadsheetOca extends Component {
    setup() {
        this.router = useService("router");
        this.orm = useService("orm");
        const params = this.props.action.params || this.props.action.context.params;
        this.spreadsheetId = params.spreadsheet_id;
        this.model = params.model || "spreadsheet.spreadsheet";
        this.import_data = params.import_data || {};
        onMounted(() => {
            this.router.pushState({
                spreadsheet_id: this.spreadsheetId,
                model: this.model,
            });
        });
        onWillStart(async () => {
            this.record =
                (await this.orm.call(
                    this.model,
                    "get_spreadsheet_data",
                    [[this.spreadsheetId]],
                    {context: {bin_size: false}}
                )) || {};
        });
        useSubEnv({
            saveRecord: this.saveRecord.bind(this),
            importData: this.importData.bind(this),
        });
    }
    async saveRecord(data) {
        if (this.record.mode === "readonly") {
            return;
        }
        if (this.spreadsheetId) {
            this.orm.call(this.model, "write", [this.spreadsheetId, data]);
        } else {
            this.spreadsheetId = await this.orm.call(this.model, "create", [data]);
            this.router.pushState({spreadsheet_id: this.spreadsheetId});
        }
    }

    async importDataGraph(spreadsheet_model) {
        var sheetId = spreadsheet_model.getters.getActiveSheetId();
        var y = 0;
        if (this.import_data.new === undefined && this.import_data.new_sheet) {
            sheetId = uuidGenerator.uuidv4();
            spreadsheet_model.dispatch("CREATE_SHEET", {
                sheetId,
                position: spreadsheet_model.getters.getSheetIds().length,
            });
            // We want to open the new sheet
            const sheetIdFrom = spreadsheet_model.getters.getActiveSheetId();
            spreadsheet_model.dispatch("ACTIVATE_SHEET", {
                sheetIdFrom,
                sheetIdTo: sheetId,
            });
        } else if (this.import_data.new === undefined) {
            // TODO: Add a way to detect the last row total height
        }
        const dataSourceId = uuidGenerator.uuidv4();
        const definition = {
            title: this.import_data.metaData.title,
            type: "odoo_" + this.import_data.metaData.mode,
            background: "#FFFFFF",
            stacked: this.import_data.metaData.stacked,
            metaData: this.import_data.metaData,
            searchParams: this.import_data.searchParams,
            dataSourceId: dataSourceId,
            legendPosition: "top",
            verticalAxisPosition: "left",
        };
        spreadsheet_model.dispatch("CREATE_CHART", {
            sheetId,
            id: dataSourceId,
            position: {
                x: 0,
                y: y,
            },
            definition,
        });
    }
    async importDataPivot(spreadsheet_model) {
        var sheetId = spreadsheet_model.getters.getActiveSheetId();
        var row = 0;
        if (this.import_data.new === undefined && this.import_data.new_sheet) {
            sheetId = uuidGenerator.uuidv4();
            spreadsheet_model.dispatch("CREATE_SHEET", {
                sheetId,
                position: spreadsheet_model.getters.getSheetIds().length,
            });
            // We want to open the new sheet
            const sheetIdFrom = spreadsheet_model.getters.getActiveSheetId();
            spreadsheet_model.dispatch("ACTIVATE_SHEET", {
                sheetIdFrom,
                sheetIdTo: sheetId,
            });
        } else if (this.import_data.new === undefined) {
            row = spreadsheet_model.getters.getNumberRows(sheetId);
            var maxcols = spreadsheet_model.getters.getNumberCols(sheetId);
            var filled = false;
            while (row >= 0) {
                for (var col = maxcols; col >= 0; col--) {
                    if (
                        spreadsheet_model.getters.getCell(sheetId, col, row) !==
                            undefined &&
                        !spreadsheet_model.getters.getCell(sheetId, col, row).isEmpty()
                    ) {
                        filled = true;
                        break;
                    }
                }
                if (filled) {
                    break;
                }
                row -= 1;
            }
            row += 1;
        }
        const dataSourceId = uuidGenerator.uuidv4();
        const pivot_info = {
            metaData: {
                colGroupBys: this.import_data.metaData.colGroupBys,
                rowGroupBys: this.import_data.metaData.rowGroupBys,
                activeMeasures: this.import_data.metaData.activeMeasures,
                resModel: this.import_data.metaData.resModel,
            },
            searchParams: this.import_data.searchParams,
        };
        const dataSource = spreadsheet_model.config.dataSources.add(
            dataSourceId,
            PivotDataSource,
            pivot_info
        );
        await dataSource.load();
        const {cols, rows, measures} = dataSource.getTableStructure().export();
        const table = {
            cols,
            rows,
            measures,
        };
        spreadsheet_model.dispatch("INSERT_PIVOT", {
            sheetId,
            col: 0,
            row: row,
            id: spreadsheet_model.getters.getNextPivotId(),
            table,
            dataSourceId,
            definition: pivot_info,
        });
    }
    async importData(spreadsheet_model) {
        if (this.import_data.mode === "pivot") {
            await this.importDataPivot(spreadsheet_model);
        }
        if (this.import_data.mode === "graph") {
            await this.importDataGraph(spreadsheet_model);
        }
    }
}
ActionSpreadsheetOca.template = "spreadsheet_oca.ActionSpreadsheetOca";
ActionSpreadsheetOca.components = {
    SpreadsheetRenderer,
    SpreadsheetControlPanel,
};
actionRegistry.add("action_spreadsheet_oca", ActionSpreadsheetOca, {force: true});
