module.exports = {
    name: '@1ai/1ai-skills-bundle',
    version: '1.0.0',
    description: 'Install all 80+ 1ai-skills with a single command',
    getSkillIndex: require('./skill-index.json'),
    install: require('./install-skills'),
    list: require('./list-skills'),
    verify: require('./verify-install')
};
