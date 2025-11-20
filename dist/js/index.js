"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __exportStar = (this && this.__exportStar) || function(m, exports) {
    for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(exports, p)) __createBinding(exports, m, p);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.allApplications = exports.templateStaticMixin = exports.templateMixin = exports.applicationStaticMixin = exports.applicationMixin = exports.flavorMixin = exports.executableMixin = exports.JSONSchemaFormDataProvider = exports.ContextProvider = exports.ApplicationRegistry = exports.Template = exports.Flavor = exports.Executable = exports.Application = void 0;
const application_1 = __importDefault(require("./application"));
exports.Application = application_1.default;
const applicationMixin_1 = require("./applicationMixin");
Object.defineProperty(exports, "applicationMixin", { enumerable: true, get: function () { return applicationMixin_1.applicationMixin; } });
Object.defineProperty(exports, "applicationStaticMixin", { enumerable: true, get: function () { return applicationMixin_1.applicationStaticMixin; } });
const ApplicationRegistry_1 = __importDefault(require("./ApplicationRegistry"));
exports.ApplicationRegistry = ApplicationRegistry_1.default;
const ContextProvider_1 = __importDefault(require("./context/ContextProvider"));
exports.ContextProvider = ContextProvider_1.default;
const JSONSchemaFormDataProvider_1 = __importDefault(require("./context/JSONSchemaFormDataProvider"));
exports.JSONSchemaFormDataProvider = JSONSchemaFormDataProvider_1.default;
const executable_1 = __importDefault(require("./executable"));
exports.Executable = executable_1.default;
const executableMixin_1 = require("./executableMixin");
Object.defineProperty(exports, "executableMixin", { enumerable: true, get: function () { return executableMixin_1.executableMixin; } });
const flavor_1 = __importDefault(require("./flavor"));
exports.Flavor = flavor_1.default;
const flavorMixin_1 = require("./flavorMixin");
Object.defineProperty(exports, "flavorMixin", { enumerable: true, get: function () { return flavorMixin_1.flavorMixin; } });
const template_1 = __importDefault(require("./template"));
exports.Template = template_1.default;
const templateMixin_1 = require("./templateMixin");
Object.defineProperty(exports, "templateMixin", { enumerable: true, get: function () { return templateMixin_1.templateMixin; } });
Object.defineProperty(exports, "templateStaticMixin", { enumerable: true, get: function () { return templateMixin_1.templateStaticMixin; } });
const allApplications = ApplicationRegistry_1.default.getUniqueAvailableApplicationNames();
exports.allApplications = allApplications;
__exportStar(require("./types"), exports);
