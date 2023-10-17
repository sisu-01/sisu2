const watchdog = new CKSource.EditorWatchdog();

window.watchdog = watchdog;

watchdog.setCreator( ( element, config ) => {
	return CKSource.Editor
		.create( element, config )
		.then( editor => {
			return editor;
		} );
} );

watchdog.setDestructor( editor => {
	return editor.destroy();
} );

watchdog.on( 'error', handleSampleError );

watchdog
.create( document.querySelector("#editor"), {
	simpleUpload: {
		uploadUrl: UPLOAD_URL,

		// Enable the XMLHttpRequest.withCredentials property.
		withCredentials: true,

		// Headers sent along with the XMLHttpRequest to the upload server.
		headers: {
			"X-CSRFToken": CSRF_TOKEN,
			Authorization: "Bearer <JSON Web Token>"
		}
	}
} )
.then( editor => {
	window.editor = editor;
} )
.catch( handleSampleError );

function handleSampleError( error ) {
	const issueUrl = 'https://github.com/ckeditor/ckeditor5/issues';

	const message = [
		'Oops, something went wrong!',
		`Please, report the following error on ${ issueUrl } with the build id "edsteai8845-ktylh53u5b3o" and the error stack trace:`
	].join( '\n' );

	console.error( message );
	console.error( error );
}
