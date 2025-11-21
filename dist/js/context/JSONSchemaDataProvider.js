"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const ContextProvider_1 = __importDefault(require("./ContextProvider"));
/**
 * @summary Provides jsonSchema only.
 */
class JSONSchemaDataProvider extends ContextProvider_1.default {
    constructor(config) {
        super(config);
        this.isUsingJinjaVariables = Boolean(config === null || config === void 0 ? void 0 : config.isUsingJinjaVariables);
    }
    get jsonSchema() {
        throw new Error("Not implemented.");
    }
}
exports.default = JSONSchemaDataProvider;
