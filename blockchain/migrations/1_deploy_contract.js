



let Contract = artifacts.require("ElectricityMeterReading");
const fs = require('fs')

module.exports = async function (deployer) {
  await deployer.deploy(Contract , "Hulk");
  const deployedCertification = await Contract.deployed();
  let configData = {};
  configData.address = deployedCertification.address;
  fs.writeFileSync('./deployment_config.json', JSON.stringify(configData, null, 2));
  console.log(`Certification contract deployed at address: ${deployedCertification.address}`);
};