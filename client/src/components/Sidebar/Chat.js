import React from "react";
import { Box } from "@material-ui/core";
import { BadgeAvatar, ChatContent, UnreadMessages } from "../Sidebar";
import { makeStyles } from "@material-ui/core/styles";
import { setActiveChat } from "../../store/activeConversation";
import { connect } from "react-redux";
import { qtyUnreadReset, fetchConversations} from "../../store/utils/thunkCreators";

const useStyles = makeStyles((theme) => ({
  root: {
    borderRadius: 8,
    height: 80,
    boxShadow: "0 2px 10px 0 rgba(88,133,196,0.05)",
    marginBottom: 10,
    display: "flex",
    alignItems: "center",
    "&:hover": {
      cursor: "grab"
    }
  }
}));

const Chat = (props) => {
  const classes = useStyles();
  const { conversation, qtyUnreadReset, fetchConversations } = props;
  const { otherUser } = conversation;

  const handleClick = async (conversation) => {
    // reset the unread message counter to 0.
    await qtyUnreadReset(conversation.id);
    await fetchConversations();
    await props.setActiveChat(conversation.otherUser.username);
  };

  return (
    <Box onClick={() => handleClick(conversation)} className={classes.root}>
      <BadgeAvatar
        photoUrl={otherUser.photoUrl}
        username={otherUser.username}
        online={otherUser.online}
        sidebar={true}
      />
      <ChatContent conversation={conversation} />
      <UnreadMessages qty={conversation.qtyUnread}/>
    </Box>
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    setActiveChat: (id) => {
      dispatch(setActiveChat(id));
    },
    qtyUnreadReset: (conversation) => {
      dispatch(qtyUnreadReset(conversation));
    },
    fetchConversations: () => {
      dispatch(fetchConversations());
    }
  };
};

export default connect(null, mapDispatchToProps)(Chat);
