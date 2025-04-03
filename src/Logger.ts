import chalk from 'chalk';

export default class Logger {
    private static logExecutionTime(fn: Function, args: any[]): { result: any, duration: number } {
        const start = Date.now();
        const result = fn(...args);
        const end = Date.now();
        const duration = end - start;
        return {result, duration};
    }

    static runFunction(fn: Function, ...args: any[]): void {
        const timestamp = new Date().toISOString();

        try {
            const {result, duration} = Logger.logExecutionTime(fn, args);
            const logMessage = `[${timestamp}] [${fn.name}] - Execution Time: ${duration}ms`;
            console.log(chalk.green(logMessage), result);
        } catch (error) {
            const errorMessage = `[${timestamp}] [${fn.name}] - ${chalk.red('[ERROR]')} - ${error}`;
            console.error(errorMessage, error);
        }
    }
}
