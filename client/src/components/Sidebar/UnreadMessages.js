import React from "react";
import { Box, Badge } from "@material-ui/core";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles(() => ({
  unreadMessages: {
    backgroundColor: "#3F92FF",
    right: 40
  },
}));

const UnreadMessages = (props) => {
  const classes = useStyles();
  const { qty } = props;
  return (
    <Box>
      <Badge
        badgeContent = { qty }
        max = {99}
        color="primary"
        classes={{ badge: `${classes.unreadMessages}` }}
        >
      </Badge>
    </Box>
  );
};

export default UnreadMessages;
