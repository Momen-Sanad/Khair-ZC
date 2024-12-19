#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Define the instance name and port
INSTANCE_NAME="sql_server_khair"
PORT=1434

# Function to check if Docker is running
check_docker() {
    if ! systemctl is-active --quiet docker; then
        echo -e "${YELLOW}Docker is not running. Starting Docker...${NC}"
        sudo systemctl start docker
        sleep 2
    fi
}

# Function to check if the "khair" container exists
check_container() {
    if sudo docker ps -a | grep -q "$INSTANCE_NAME"; then
        return 0
    else
        return 1
    fi
}

# Function to start the "khair" SQL Server
start_sql_server_khair() {
    echo -e "${YELLOW}Starting SQL Server instance 'khair'...${NC}"

    if check_container; then
        if [ "$(sudo docker ps -q -f name=$INSTANCE_NAME)" ]; then
            echo -e "${GREEN}SQL Server 'khair' is already running!${NC}"
        else
            sudo docker start $INSTANCE_NAME
            echo -e "${GREEN}SQL Server 'khair' container started!${NC}"
        fi
    else
        echo "Creating new SQL Server container for 'khair'..."
        sudo docker run -e "ACCEPT_EULA=Y" \
            -e "MSSQL_SA_PASSWORD=YourStrong@Passw0rd" \
            -e "MSSQL_PID=Developer" \
            --name $INSTANCE_NAME \
            --hostname $INSTANCE_NAME \
            -p $PORT:1433 \
            --restart unless-stopped \
            -u 0 \
            -d mcr.microsoft.com/mssql/server:2022-latest

        echo -e "${GREEN}New SQL Server 'khair' container created and started!${NC}"
    fi

    echo -e "\n${GREEN}Connection Details for Azure Data Studio:${NC}"
    echo -e "Server: 127.0.0.1,$PORT"
    echo -e "Authentication: SQL Login"
    echo -e "Username: SA"
    echo -e "Password: YourStrong@Passw0rd"
    echo -e "Remember to check 'Trust server certificate'"
}

# Function to stop the "khair" SQL Server
stop_sql_server_khair() {
    if check_container; then
        echo -e "${YELLOW}Stopping SQL Server instance 'khair'...${NC}"
        sudo docker stop $INSTANCE_NAME
        echo -e "${GREEN}SQL Server 'khair' stopped!${NC}"
    else
        echo -e "${RED}SQL Server 'khair' container not found!${NC}"
    fi
}

# Function to show "khair" SQL Server status
show_status() {
    if check_container; then
        echo -e "${YELLOW}SQL Server 'khair' container status:${NC}"
        sudo docker ps -a | grep $INSTANCE_NAME
    else
        echo -e "${RED}SQL Server 'khair' container not found!${NC}"
    fi
}

# Main menu
show_menu() {
    echo -e "\n${GREEN}SQL Server 'Khair' Manager${NC}"
    echo "1. Start SQL Server 'khair'"
    echo "2. Stop SQL Server 'khair'"
    echo "3. Show Status"
    echo "4. Exit"
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Main loop
while true; do
    check_docker
    show_menu
    read -p "Enter your choice (1-4): " choice

    case $choice in
        1)
            start_sql_server_khair
            ;;
        2)
            stop_sql_server_khair
            ;;
        3)
            show_status
            ;;
        4)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid choice. Please try again.${NC}"
            ;;
    esac

    echo -e "\nPress Enter to continue..."
    read
done
