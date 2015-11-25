// http://stackoverflow.com/questions/13013387/clearing-the-serial-ports-buffer

int open_port(void)
{
  int fd; /* File descriptor for the port */

  fd = open("/dev/ttyUSB0", O_RDWR | O_NOCTTY | O_NDELAY);

  if (fd == -1)
  {
   // Could not open the port.          
   perror("open_port: Unable to open /dev/ttyUSB0 - ");
  }
  else
    fcntl(fd, F_SETFL, 0);

  struct termios options;

  tcgetattr(fd, &options); 
  //setting baud rates and stuff
  cfsetispeed(&options, B19200);
  cfsetospeed(&options, B19200);
  options.c_cflag |= (CLOCAL | CREAD);
  tcsetattr(fd, TCSANOW, &options);

  tcsetattr(fd, TCSAFLUSH, &options);

  options.c_cflag &= ~PARENB;//next 4 lines setting 8N1
  options.c_cflag &= ~CSTOPB;
  options.c_cflag &= ~CSIZE;
  options.c_cflag |= CS8;

  //options.c_cflag &= ~CNEW_RTSCTS;

  options.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); //raw input

  options.c_iflag &= ~(IXON | IXOFF | IXANY); //disable software flow control

  sleep(2); //required to make flush work, for some reason
  tcflush(fd,TCIOFLUSH);

  return (fd);
}
