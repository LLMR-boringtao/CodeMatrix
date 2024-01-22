# Backend
pdm install
pdm run start
pdm run test
brew install postgresql
brew services start postgresql
createuser -s postgres
pdm run recreate-db