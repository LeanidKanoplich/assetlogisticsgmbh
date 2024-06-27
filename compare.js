const fs = require('fs');
const diff = require('diff');

// Цветовые коды ANSI
const COLOR_RESET = '\x1b[0m';
const COLOR_GREEN = '\x1b[32m';
const COLOR_RED = '\x1b[31m';

// Функция для чтения файла
function readFile(filePath) {
    return new Promise((resolve, reject) => {
        fs.readFile(filePath, 'utf8', (err, data) => {
            if (err) {
                return reject(err);
            }
            resolve(data);
        });
    });
}

// Функция для записи файла
function writeFile(filePath, data) {
    return new Promise((resolve, reject) => {
        fs.writeFile(filePath, data, 'utf8', (err) => {
            if (err) {
                return reject(err);
            }
            resolve();
        });
    });
}

// Основная функция для сравнения файлов и сохранения изменений
async function compareAndSaveFiles(file1, file2, outputFile) {
    try {
        const [data1, data2] = await Promise.all([readFile(file1), readFile(file2)]);

        console.log(`Comparing files:\n${file1}\n${file2}\n`);

        const differences = diff.diffLines(data1, data2);
        let result = '';

        differences.forEach((part) => {
            const color = part.added ? COLOR_GREEN : part.removed ? COLOR_RED : COLOR_RESET;
            const symbol = part.added ? '++ ' : part.removed ? '-- ' : '   ';
            const lines = part.value.split('\n');

            lines.forEach((line) => {
                if (line.trim() || line === '') {
                    const outputLine = `${color}${symbol}"${line}"${COLOR_RESET}`.trim();
                    result += outputLine + '\n';
                    process.stdout.write(outputLine + '\n');
                }
            });
        });

        console.log(COLOR_RESET); // Сброс цвета

        await writeFile(outputFile, result);
        console.log(`Changes saved to ${outputFile}`);
    } catch (err) {
        console.error('Error reading or writing files:', err);
    }
}

// Путь к файлам
const file1 = process.argv[2];
const file2 = process.argv[3];
const outputFile = process.argv[4] || 'app3.py';

if (!file1 || !file2) {
    console.error('Please provide two file paths to compare');
    process.exit(1);
}

compareAndSaveFiles(file1, file2, outputFile);
